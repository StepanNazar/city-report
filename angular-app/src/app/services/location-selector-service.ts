import {Injectable} from '@angular/core';

export interface LocationOption {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

@Injectable({
  providedIn: 'root'
})
export abstract class LocationSelectorService {
  abstract searchLocations(country: string, state: string, locality: string): Promise<LocationOption[]>;
}
