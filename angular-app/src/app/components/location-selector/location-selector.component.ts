import { Component, signal, inject, output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LocationOption, LocationSelectorService, ReverseGeocodingResult } from '../../services/location-selector-service';


@Component({
  selector: 'app-location-selector',
  imports: [FormsModule],
  templateUrl: './location-selector.component.html',
  styleUrl: './location-selector.component.scss'
})
export class LocationSelector {
  private locationSelectorService = inject(LocationSelectorService);

  localityOptions: LocationOption[] = [];
  readonly typedInCountry = signal<string>("");
  readonly typedInState = signal<string>("");
  readonly typedInLocality = signal<string>("");
  readonly selectedLocation = signal<LocationOption | null>(null);
  readonly locationSelectedEvent = output<LocationOption | null>();
  readonly isLoading = signal<boolean>(false);
  readonly error = signal<string | null>(null);

  /**
   * Populate fields with reverse geocoded data and trigger search
   */
  async populateFromReverseGeocode(geocodeData: ReverseGeocodingResult) {
    const country = geocodeData.country;
    const state = geocodeData.state;
    const city = geocodeData.city;

    this.typedInCountry.set(country);
    this.typedInState.set(state);
    this.typedInLocality.set(city);

    // Automatically trigger search with populated data
    if (country || state || city) {
      await this.onSearch();
    }
  }

  async onSearch() {
    if (this.isLoading()) {
      return;
    }
    if (this.typedInCountry() === "" && this.typedInState() === "" && this.typedInLocality() === "") {
      return;
    }

    this.isLoading.set(true);
    this.error.set(null);
    try {
      this.localityOptions = await this.locationSelectorService.searchLocations(
        this.typedInCountry(), this.typedInState(), this.typedInLocality()
      );
    } catch (err) {
      this.error.set('Error loading locations');
      this.localityOptions = [];
    } finally {
      this.isLoading.set(false);
      this.selectedLocation.set(this.localityOptions[0] || null);
      this.onSelectLocation();
    }
  }

  onSelectLocation() {
    this.locationSelectedEvent.emit(this.selectedLocation());
  }
}
