import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ImageResponse {
    id: string;
    url: string;
}

export interface CreateSolutionPayload {
    title: string;
    body: string;
    imagesIds?: string[];
}

export interface SolutionResponse {
    id: number;
    authorId: number;
    authorLink: string;
    authorFirstName: string;
    authorLastName: string;
    title: string;
    body: string;
    images: ImageResponse[];
    createdAt: string;
    updatedAt: string;
    likes: number;
    dislikes: number;
    comments: number;
    approved: boolean;
    approvedAt?: string;
}

export interface SolutionsResponse {
    hasNext: boolean;
    hasPrev: boolean;
    items: SolutionResponse[];
    itemsPerPage: number;
    links: {
        self: string;
        first: string;
        prev?: string;
        next?: string;
        last: string;
    };
    page: number;
    totalItems: number;
    totalPages: number;
}

@Injectable({
    providedIn: 'root'
})
export class SolutionsService {
    private http = inject(HttpClient);

    createSolution(postId: number, payload: CreateSolutionPayload): Observable<SolutionResponse> {
        return this.http.post<SolutionResponse>(`/api/posts/${postId}/solutions`, payload);
    }

    getSolutions(
        postId: number,
        page: number = 1,
        perPage: number = 5,
        sortBy: string = 'likes',
        order: string = 'desc',
        approved?: boolean
    ): Observable<SolutionsResponse> {
        let params = new HttpParams();
        params = params.append('page', page.toString());
        params = params.append('per_page', perPage.toString());
        params = params.append('sort_by', sortBy);
        params = params.append('order', order);

        if (approved !== undefined) {
            params = params.append('approved', approved.toString());
        }

        return this.http.get<SolutionsResponse>(`/api/posts/${postId}/solutions`, { params });
    }

    getSolution(solutionId: number): Observable<SolutionResponse> {
        return this.http.get<SolutionResponse>(`/api/solutions/${solutionId}`);
    }

    updateSolution(solutionId: number, payload: CreateSolutionPayload): Observable<SolutionResponse> {
        return this.http.put<SolutionResponse>(`/api/solutions/${solutionId}`, payload);
    }

    deleteSolution(solutionId: number): Observable<void> {
        return this.http.delete<void>(`/api/solutions/${solutionId}`);
    }

    approveSolution(solutionId: number): Observable<void> {
        return this.http.put<void>(`/api/solutions/${solutionId}/approval`, {});
    }

    removeApproval(solutionId: number): Observable<void> {
        return this.http.delete<void>(`/api/solutions/${solutionId}/approval`);
    }
}
