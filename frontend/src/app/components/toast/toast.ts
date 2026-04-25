// toast.component.ts
import { Component, inject } from '@angular/core';
import { ToastService } from './toast.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-toast',
  standalone: true,
  templateUrl: './toast.html',
  styleUrls: ['./toast.css'],
  imports: [CommonModule,FormsModule],
})
export class ToastComponent {

  toastService = inject(ToastService);

  getToasts() {
    return this.toastService.toasts();
  }

  trackById(index: number, item: any) {
    return item.id;
  }
}
