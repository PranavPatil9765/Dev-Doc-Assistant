import { Component, signal, effect } from '@angular/core';

@Component({
  selector: 'app-landing-page',
  standalone: true,
  templateUrl: './landing-page.html',
  styleUrls: ['./landing-page.css']
})
export class LandingPageComponent {
  title = signal('Developer Documentation Assistant');
  subtitleFull = 'Understand codebases. Debug faster. Build smarter.';
  subtitle = signal('');

  constructor() {
    this.typeWriterEffect();
  }

  typeWriterEffect() {
    let i = 0;
    const interval = setInterval(() => {
      if (i < this.subtitleFull.length) {
        this.subtitle.set(this.subtitle() + this.subtitleFull[i]);
        i++;
      } else {
        clearInterval(interval);
      }
    }, 40);
  }

  startSession() {
    console.log('Session Started');
  }
}

