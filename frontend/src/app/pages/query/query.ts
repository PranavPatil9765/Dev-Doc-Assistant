import { Component, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

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


  constructor(private http: HttpClient) {}

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
        },
        error: () => {
          // ❌ mark error
          this.files.update(f =>
            f.map(item =>
              item.file === file ? { ...item, status: 'error' } : item
            )
          );
        }
      });

    });

    input.value = '';
  }
}


  sendMessage() {
    const text = this.inputText().trim();
    if (!text) return;

    const sessionId = sessionStorage.getItem('sessionId');

    this.messages.update(m => [...m, { role: 'user', content: text }]);
    this.inputText.set('');
    this.isLoading.set(true);

    this.http.post<{ answer: string }>('/api/query', {
      question: text,
      session_id: sessionId
    }).subscribe({
      next: (res) => {
        this.messages.update(m => [...m, { role: 'assistant', content: res.answer }]);
        this.isLoading.set(false);
      },
      error: () => {
        this.messages.update(m => [...m, { role: 'assistant', content: 'Error fetching response.' }]);
        this.isLoading.set(false);
      }
    });
  }

  newSession() {
    sessionStorage.removeItem('sessionId');
    location.reload();
  }
}
