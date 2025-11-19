import { inject, Injectable, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { LocationProvider } from './location-selector-service';

interface RegisterPayload {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  localityId: number | undefined;
  localityProvider: LocationProvider | undefined;
}

interface LoginPayload {
  email: string;
  password: string;
}

export interface AccessTokenResponse {
  access_token: string;
}

export interface WhoAmIResponse {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  is_activated: boolean;
  localityLongitude: number | undefined;
  localityLatitude: number | undefined;
  locality_nominatim_id: number | undefined;
  locality_google_id: number | undefined;
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  http = inject(HttpClient);
  cookieService = inject(CookieService);

  isAuthenticated = signal(!!this.getUserId());

  setAccessToken(token: string) {
    localStorage.setItem('d97g4584V5D6dg65gHDRG546r9d56', token);
    this.isAuthenticated.set(true);
  }
  getAccessToken(): string | null {
    return localStorage.getItem('d97g4584V5D6dg65gHDRG546r9d56');
  }
  clearAccessToken() {
    localStorage.removeItem('d97g4584V5D6dg65gHDRG546r9d56');
    this.isAuthenticated.set(false);
  }
  getUserId(): string | null {
    const token = this.getAccessToken();
    if (token) {
      const parts = token.split('.');
      if (parts.length === 3) {
        const payload = JSON.parse(atob(parts[1]));
        return payload.sub;
      }
    }
    return null;
  }
  register(payload: RegisterPayload): Observable<AccessTokenResponse> {
    return this.http.post<AccessTokenResponse>('/api/auth/register', payload).pipe(
      tap(response => {
        this.setAccessToken(response.access_token);
      })
    );
  }
  login(payload: LoginPayload): Observable<AccessTokenResponse> {
    return this.http.post<AccessTokenResponse>('/api/auth/login', payload).pipe(
      tap(response => {
        this.setAccessToken(response.access_token);
      })
    );
  }
  refresh(): Observable<AccessTokenResponse> {
    const csrfToken = this.cookieService.get('csrf_refresh_token');
    const options = csrfToken
      ? { headers: { 'X-CSRF-TOKEN': csrfToken } }
      : {};
    return this.http.post<AccessTokenResponse>('/api/auth/refresh', {}, options).pipe(
      tap(response => {
        this.setAccessToken(response.access_token);
      })
    );
  }
  logout() {
    let observable = this.http.post('/api/auth/logout', {});
    this.clearAccessToken();
    return observable;
  }
  whoami(): Observable<WhoAmIResponse> {
    return this.http.get<WhoAmIResponse>('/api/auth/whoami');
  }
}
