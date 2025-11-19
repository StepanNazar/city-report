import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LocationProvider } from './location-selector-service';

export interface CreatePostPayload {
    latitude: number;
    longitude: number;
    title: string;
    body: string;
    imagesIds?: string[];
    localityId: number;
    localityProvider: LocationProvider;
}

export interface PostResponse {
    id: number;
    authorId: number;
    authorLink: string;
    authorFirstName: string;
    authorLastName: string;
    latitude: number;
    longitude: number;
    title: string;
    body: string;
    images: string[];
    localityNominatimId?: number;
    localityGoogleId?: number;
    createdAt: string;
    updatedAt: string;
    likes: number;
    dislikes: number;
    comments: number;
}

@Injectable({
    providedIn: 'root'
})
export class PostsService {
    private http = inject(HttpClient);

    createPost(payload: CreatePostPayload): Observable<PostResponse> {
        return this.http.post<PostResponse>('/api/posts', payload);
    }

    getPost(postId: number): Observable<PostResponse> {
        return this.http.get<PostResponse>(`/api/posts/${postId}`);
    }

    updatePost(postId: number, payload: CreatePostPayload): Observable<PostResponse> {
        return this.http.put<PostResponse>(`/api/posts/${postId}`, payload);
    }

    deletePost(postId: number): Observable<void> {
        return this.http.delete<void>(`/api/posts/${postId}`);
    }
}

