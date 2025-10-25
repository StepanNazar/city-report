import { Component } from '@angular/core';
import { ImageUpload } from '../image-upload/image-upload';
import { LocationChoiceComponent } from '../location-choice-component/location-choice-component';

@Component({
  selector: 'app-post-edit',
  imports: [ImageUpload, LocationChoiceComponent],
  templateUrl: './post-edit.html',
  styleUrl: './post-edit.scss'
})
export class PostEdit {

}
