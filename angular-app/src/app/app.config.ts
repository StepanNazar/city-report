import { ApplicationConfig, provideBrowserGlobalErrorListeners, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { LocationSelectorService } from './location-selector/location-selector-service';
import { NominatimLocationSelectorService } from './location-selector/nominatim-location-selector.service';

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    { provide: LocationSelectorService, useClass: NominatimLocationSelectorService },
  ]
};
