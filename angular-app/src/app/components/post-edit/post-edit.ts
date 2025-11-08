import { Component } from '@angular/core';
import { ImageUpload } from '../image-upload/image-upload';
import { LocationSelector } from '../location-selector/location-selector.component';

@Component({
  selector: 'app-post-edit',
  imports: [ImageUpload, LocationSelector],
  templateUrl: './post-edit.html',
  styleUrl: './post-edit.scss'
})
export class PostEdit {

}
