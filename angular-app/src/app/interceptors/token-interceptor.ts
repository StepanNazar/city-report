import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthenticationService } from '../services/authentication-service';
import {catchError, Observable, switchMap, throwError} from 'rxjs';


function isJWTError(error: HttpErrorResponse) {
  return (error.status === 400 && error.error?.msg === "User claims verification failed") ||
         (error.status === 401) ||
         (error.status === 422 && error.error?.message !== "Validation error")
}

export const tokenInterceptor: HttpInterceptorFn = (req, next) => {
  if (
    req.url.endsWith('/auth/refresh') ||
    req.url.endsWith('/auth/register') ||
    req.url.endsWith('/auth/login')
  ) {
    return next(req);
  }

  const authService = inject(AuthenticationService);

  const addToken = (request: typeof req, accessToken: string) => {
    return request.clone({
      setHeaders: {
        Authorization: `Bearer ${accessToken}`
      }
    });
  };

  const handleRefreshError = (refreshError: HttpErrorResponse) => {
    if (isJWTError(refreshError)) {
      authService.clearAccessToken();
    }
    return throwError(() => refreshError);
  };

  const RefreshTokenAndRetry = (): Observable<any> => {
    return authService.refresh().pipe(
      switchMap((response) => {
        const retryReq = addToken(req, response.access_token);
        return next(retryReq);
      }),
      catchError(handleRefreshError)
    );
  };

  const token = authService.getAccessToken();

  if (token) {
    const newReq = addToken(req, token);
    return next(newReq).pipe(
      catchError((error: HttpErrorResponse) => {
        return isJWTError(error) ? RefreshTokenAndRetry() : throwError(() => error);
      })
    );
  }

  return RefreshTokenAndRetry();
};
