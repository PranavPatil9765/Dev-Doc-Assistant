import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/landing-page/landing-page')
      .then(m => m.LandingPageComponent)},
  {
    path: 'query',
    loadComponent: () => import('./pages/query/query')
      .then(m => m.QueryComponent)}
];
