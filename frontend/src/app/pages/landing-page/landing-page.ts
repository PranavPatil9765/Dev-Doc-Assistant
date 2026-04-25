// landing-page.component.ts

import { Component, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastService } from '../../components/toast/toast.service'; // adjust path

@Component({
  selector: 'app-landing-page',
  standalone: true,
  templateUrl: './landing-page.html',
  styleUrls: ['./landing-page.css']
})
export class LandingPageComponent {

  title = signal('Developer Documentation Assistant');
  subtitle = signal('Query your documents. Understand your code.');

  isLoading = signal(false);

  constructor(
    private http: HttpClient,
    private toast: ToastService
  ) {}

  startSession() {
    this.isLoading.set(true);

    this.http.post<{ session_id: string }>('/api/create-session', {})
      .subscribe({
        next: (res) => {
          sessionStorage.setItem('sessionId', res.session_id);

          this.isLoading.set(false);

          this.toast.show('Session created successfully', 'success');
          console.log('Session created with ID:', res.session_id);
        },
        error: (err) => {
          this.isLoading.set(false);

          this.toast.show('Failed to create session. Please try again.', 'error');

          console.error('Session creation failed', err);
        }
      });
  }
}
