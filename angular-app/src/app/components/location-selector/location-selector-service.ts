import {Injectable} from '@angular/core';
import {LocationOption} from './location-option';

@Injectable({
  providedIn: 'root'
})
export abstract class LocationSelectorService {
  abstract searchLocations(country: string, state: string, locality: string): Promise<LocationOption[]>;
}
