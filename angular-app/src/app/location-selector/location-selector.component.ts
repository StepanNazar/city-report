import {Component, signal, inject, output} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {LocationOption} from './location-option';
import {LocationSelectorService} from './location-selector-service';


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

  onSearch() {
    this.locationSelectorService.searchLocations(
      this.typedInCountry(),
      this.typedInState(),
      this.typedInLocality()
    ).then(options => {
      this.localityOptions = options;
      this.selectedLocation.set(options[0] || null);
      this.onSelectLocation();
    });
  }
  onSelectLocation() {
    this.locationSelectedEvent.emit(this.selectedLocation());
  }
}
