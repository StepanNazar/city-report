import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { LocationProvider } from './location-selector-service';

export interface ImageResponse {
    id: string;
    url: string;
}

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
    images: ImageResponse[];
    localityNominatimId?: number;
    localityGoogleId?: number;
    createdAt: string;
    updatedAt: string;
    likes: number;
    dislikes: number;
    comments: number;
}

export interface PostsResponse {
    hasNext: boolean;
    hasPrev: boolean;
    items: PostResponse[];
    itemsPerPage: number;
    links: {
        self: string;
        first: string;
        prev?: string;
        next?: string;

        last: string;
    },
    page: number;
    totalItems: number;
    totalPages: number;
}

// Map Clusters Types
export interface ClusterBounds {
    minLat: number;
    maxLat: number;
    minLng: number;
    maxLng: number;
}

export interface MapPostItem {
    type: 'post';
    id: number;
    latitude: number;
    longitude: number;
    title: string;
    authorFirstName: string | null;
    authorLastName: string | null;
    createdAt: string | null;
    thumbnailUrl: string | null;
}

export interface MapClusterItem {
    type: 'cluster';
    latitude: number;
    longitude: number;
    count: number;
    bounds: ClusterBounds;
}

export type MapItem = MapPostItem | MapClusterItem;

export interface MapClustersResponse {
    items: MapItem[];
    totalInView: number;
}

@Injectable({
    providedIn: 'root'
})
export class PostsService {
    private http = inject(HttpClient);

    createPost(payload: CreatePostPayload): Observable<PostResponse> {
        return this.http.post<PostResponse>('/api/posts', payload);
    }

    getPosts(
        localityId?: number,
        localityProvider?: LocationProvider,
        page: number = 1,
        perPage: number = 20,
        sortBy: string = 'createdAt',
        order: string = 'desc'
    ): Observable<PostsResponse> {
        let params = new HttpParams();
        if (localityId && localityProvider) {
            params = params.append('localityId', localityId.toString());
            params = params.append('localityProvider', localityProvider);
        }
        params = params.append('page', page.toString());
        params = params.append('per_page', perPage.toString());
        params = params.append('sort_by', sortBy);
        params = params.append('order', order);

        return this.http.get<PostsResponse>('/api/posts', { params });
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

    getMapClusters(
        minLat: number,
        maxLat: number,
        minLng: number,
        maxLng: number,
        zoom: number
    ): Observable<MapClustersResponse> {
        const params = new HttpParams()
            .set('minLat', minLat.toString())
            .set('maxLat', maxLat.toString())
            .set('minLng', minLng.toString())
            .set('maxLng', maxLng.toString())
            .set('zoom', zoom.toString());

        return this.http.get<MapClustersResponse>('/api/posts/map-clusters', { params });
    }
}

