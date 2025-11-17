import {inject, Injectable} from '@angular/core';
import {AuthenticationService} from './authentication-service';
import {firstValueFrom} from 'rxjs';

export interface Coordinates {
  latitude: number;
  longitude: number;
}

@Injectable({
    providedIn: 'root'
})
export class GeolocationService {
    private authService = inject(AuthenticationService);

    // Default coordinates (Kyiv, Ukraine)
    private readonly defaultCoordinates: Coordinates = { latitude: 50.4501, longitude: 30.5234 };
    // Cached coordinates from whoami
    private cachedWhoamiCoordinates: Coordinates | null = null;

    /**
     * Get user's coordinates with fallback chain:
     * 1. GPS (browser geolocation)
     * 2. Cached whoami result
     * 3. Fresh whoami API call
     * 4. Default coordinates (Kyiv)
     */
    async getCurrentCoordinates(): Promise<Coordinates> {
        const gpsCoords = await this.getGPSCoordinates();
        if (gpsCoords) {
            return gpsCoords;
        }

        if (this.cachedWhoamiCoordinates) {
            return this.cachedWhoamiCoordinates;
        }

        const whoamiCoords = await this.getWhoamiCoordinates();
        if (whoamiCoords) {
            return whoamiCoords;
        }

        return this.defaultCoordinates;
    }

    /**
     * Try to get coordinates from browser's GPS/geolocation API
     */
    private async getGPSCoordinates(): Promise<Coordinates | null> {
        if (!navigator.geolocation) {
            console.log('GPS not available in this browser');
            return null;
        }

        try {
            const position = await new Promise<GeolocationPosition>((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {
                    timeout: 2000,
                });
            });

            return {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };
        } catch (error) {
            return null;
        }
    }

    /**
     * Get coordinates from /whoami API and cache them
     */
    private async getWhoamiCoordinates(): Promise<Coordinates | null> {
        try {
            const userInfo = await firstValueFrom(this.authService.whoami());

            const lat = userInfo?.localityLatitude;
            const lon = userInfo?.localityLongitude;

            if (lat !== undefined && lon !== undefined) {
                const coords = { latitude: lat, longitude: lon };
                this.cachedWhoamiCoordinates = coords;
                return coords;
            }

            console.log('User has no locality set in whoami');
            return null;
        } catch (error) {
            console.warn('Failed to get whoami coordinates:', error);
            return null;
        }
    }

    /**
     * Clear cached whoami coordinates and fetch fresh ones
     * Use this after user updates their locality
     */
    async refreshWhoamiCache(): Promise<Coordinates | null> {
        this.cachedWhoamiCoordinates = null;
        return await this.getWhoamiCoordinates();
    }

    /**
     * Clear cached whoami coordinates
     * Use this when you want to force a fresh fetch on next getCurrentCoordinates call
     */
    clearWhoamiCache(): void {
        this.cachedWhoamiCoordinates = null;
    }
}
