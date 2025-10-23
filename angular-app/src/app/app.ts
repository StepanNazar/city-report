import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {LocationSelector} from "./location-selector/location-selector.component";

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, LocationSelector],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('angular-app');
  protected readonly console = console;
}
