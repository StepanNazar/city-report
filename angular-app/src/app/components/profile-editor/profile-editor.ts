import { Component } from '@angular/core';
import { LocationSelector } from '../location-selector/location-selector.component';

@Component({
  selector: 'app-profile-editor',
  imports: [LocationSelector],
  templateUrl: './profile-editor.html',
  styleUrl: './profile-editor.scss'
})
export class ProfileEditor {

}
