import { Injectable, inject } from '@angular/core';
import { Coordinates } from '../components/map/map';
import { AuthenticationService } from './authentication-service';

@Injectable({
    providedIn: 'root'
})
export class GeolocationService {
    private authService = inject(AuthenticationService);

    /**
     * Get user's coordinates from /whoami API
     * Returns default coordinates (Kyiv) if user has no locality or API fails
     */
    async getCurrentCoordinates(): Promise<Coordinates> {
        // Default coordinates (Kyiv, Ukraine)
        const defaultCoordinates: Coordinates = {
            latitude: 50.4501,
            longitude: 30.5234
        };

        try {
            // Get user info from whoami endpoint
            const userInfo = await this.authService.whoami().toPromise();

            // Check if user has locality coordinates
            const lat = userInfo?.localityLatitude;
            const lon = userInfo?.localityLongitude;

            if (lat !== undefined && lon !== undefined) {
                return {
                    latitude: Number(lat.toFixed(6)),
                    longitude: Number(lon.toFixed(6))
                };
            }

            console.log('User has no locality set, using default coordinates');
            return defaultCoordinates;
        } catch (error) {
            console.warn('Failed to get user location from API, using default coordinates:', error);
            return defaultCoordinates;
        }
    }
}

