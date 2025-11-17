import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, forkJoin, of } from 'rxjs';

export interface ImageUploadResponse {
    id: string;
    url: string;
}

@Injectable({
    providedIn: 'root'
})
export class UploadsService {
    private http = inject(HttpClient);

    uploadImage(file: File): Observable<ImageUploadResponse> {
        const formData = new FormData();
        formData.append('image', file);

        return this.http.post<ImageUploadResponse>('/api/uploads/images', formData);
    }

    uploadMultipleImages(files: File[]): Observable<ImageUploadResponse[]> {
        if (files.length === 0) {
            return of([]);
        }

        const uploadObservables = files.map(file => this.uploadImage(file));
        return forkJoin(uploadObservables);
    }
}

