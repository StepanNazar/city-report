import {inject, Injectable} from '@angular/core';
import {Observable, tap} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {CookieService} from 'ngx-cookie-service';

interface RegisterPayload {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  localityId: number | undefined;
  localityProvider: 'google' | 'nominatim' | undefined;
}

interface AccessTokenResponse {
  access_token: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  http = inject(HttpClient);
  cookieService = inject(CookieService);

  setAccessToken(token: string) {
    localStorage.setItem('d97g4584V5D6dg65gHDRG546r9d56', token);
  }
  getAccessToken(): string | null {
    return localStorage.getItem('d97g4584V5D6dg65gHDRG546r9d56');
  }
  clearAccessToken() {
    localStorage.removeItem('d97g4584V5D6dg65gHDRG546r9d56');
  }
  register(payload: RegisterPayload): Observable<AccessTokenResponse> {
    return this.http.post<AccessTokenResponse>('/api/auth/register', payload).pipe(
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
}
