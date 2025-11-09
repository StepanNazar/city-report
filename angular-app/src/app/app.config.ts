import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { LocationSelectorService } from './services/location-selector-service';
import { NominatimLocationSelectorService } from './services/nominatim-location-selector.service';

import { routes } from './app.routes';
import {provideHttpClient, withFetch, withInterceptors} from '@angular/common/http';
import {tokenInterceptor} from './interceptors/token-interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideHttpClient(
      withFetch(), withInterceptors([tokenInterceptor]),
    ),
    provideRouter(routes),
    { provide: LocationSelectorService, useClass: NominatimLocationSelectorService },
  ]
};
