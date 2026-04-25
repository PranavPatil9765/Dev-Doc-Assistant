import { Component, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ToastService } from '../../components/toast/toast.service'; // adjust path
import { Router } from '@angular/router';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface UploadFile {
  file: File;
  status: 'uploading' | 'success' | 'error';
}

@Component({
  selector: 'app-query',
  standalone: true,
  templateUrl: './query.html',
  imports: [CommonModule]
})
export class QueryComponent {

files = signal<UploadFile[]>([]);
  messages = signal<Message[]>([]);
  inputText = signal('');
  isLoading = signal(false);
  isFetchingFiles = signal(false);

  constructor(private http: HttpClient, private toastService: ToastService, private router: Router) {
  }

 onFileSelect(event: Event) {
  const input = event.target as HTMLInputElement;

  if (input.files && input.files.length > 0) {
    const sessionId = sessionStorage.getItem('sessionId');
    if (!sessionId) return;

    const fileList = Array.from(input.files);

    fileList.forEach(file => {

      const exists = this.files().some(f =>
        f.file.name === file.name &&
        f.file.size === file.size &&
        f.file.lastModified === file.lastModified
      );

      if (exists) return;

      const uploadFile: UploadFile = {
        file,
        status: 'uploading'
      };

      this.files.update(f => [...f, uploadFile]);

      const formData = new FormData();
      formData.append('files', file);

      this.http.post(
        `/api/upload?session_id=${sessionId}`,
        formData
      ).subscribe({
        next: () => {
          this.files.update(f =>
            f.map(item =>
              item.file === file ? { ...item, status: 'success' } : item
            )
          );

          // Save to sessionStorage
          const storedFiles = JSON.parse(sessionStorage.getItem('sessionFiles') || '[]');
          storedFiles.push({ name: file.name, size: file.size, lastModified: file.lastModified });
          sessionStorage.setItem('sessionFiles', JSON.stringify(storedFiles));
        },
        error: (err) => {
          this.files.update(f =>
            f.map(item =>
              item.file === file ? { ...item, status: 'error' } : item
            )
          );
          console.log('File upload error', err);
          if (err.error) {
            this.toastService.show(err.error.detail, 'error');
          } else {
            console.error('File upload failed', err);
          }
        }
      });

    });

    input.value = '';
  }
}

goBack(){
  this.router.navigate(['/']);
}

async sendMessage() {
  const text = this.inputText().trim();
  if (!text) return;

  const sessionId = sessionStorage.getItem('sessionId');
  if (!sessionId) return;

  // add user message
  this.messages.update(m => [...m, { role: 'user', content: text }]);
  this.inputText.set('');

  // create placeholder assistant message
  let currentResponse = '';
  this.messages.update(m => [...m, { role: 'assistant', content: '' }]);

  const index = this.messages().length - 1;

  this.isLoading.set(true);

  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: text,
        session_id: sessionId
      })
    });

    if (!response.body) throw new Error('No stream');

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });

      for (let char of chunk) {
        currentResponse += char;

        this.messages.update(m => {
          const updated = [...m];
          updated[index] = {
            ...updated[index],
            content: currentResponse
          };
          return updated;
        });

        // small delay for typing effect
        await new Promise(res => setTimeout(res, 10));
      }
    }

  } catch (err) {
    console.error(err);

    this.messages.update(m => {
      const updated = [...m];
      updated[index] = {
        role: 'assistant',
        content: 'Error streaming response.'
      };
      return updated;
    });
  }

  this.isLoading.set(false);
}

  newSession() {
    this.isLoading.set(true);

    this.http.post<{ session_id: string }>('/api/create-session', {})
      .subscribe({
        next: (res) => {
          sessionStorage.setItem('sessionId', res.session_id);
          sessionStorage.removeItem('sessionFiles');

          this.files.set([]);
          this.messages.set([]);

          this.toastService.show('New session created successfully', 'success');
        },
        error: (err) => {
          this.toastService.show('Failed to create a new session. Please try again.', 'error');
          console.error('New session creation failed', err);
        },
        complete: () => {
          this.isLoading.set(false);
        }
      });
  }

  fetchSessionFiles() {
    const storedFiles = JSON.parse(sessionStorage.getItem('sessionFiles') || '[]');
    const files = storedFiles.map((file: any) => ({
      file: new File([], file.name, { lastModified: file.lastModified }),
      status: 'success'
    }));
    this.files.set(files);
  }

  ngOnInit() {
    this.fetchSessionFiles();
  }
}
