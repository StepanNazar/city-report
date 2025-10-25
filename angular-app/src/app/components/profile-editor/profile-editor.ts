import { Component } from '@angular/core';
import { LocationChoiceComponent } from '../location-choice-component/location-choice-component';

@Component({
  selector: 'app-profile-editor',
  imports: [LocationChoiceComponent],
  templateUrl: './profile-editor.html',
  styleUrl: './profile-editor.scss'
})
export class ProfileEditor {

}
