import { Injectable, inject } from '@angular/core';
import { Coordinates } from '../components/map/map';
import { AuthenticationService } from './authentication-service';
import { LocationSelectorService } from './location-selector-service';

@Injectable({
    providedIn: 'root'
})
export class GeolocationService {
    private authService = inject(AuthenticationService);
    private locationService = inject(LocationSelectorService);

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

            // Check if user has a locality with OSM ID
            const osmId = userInfo?.locality_nominatim_id;

            if (!osmId) {
                console.log('User has no locality set, using default coordinates');
                return defaultCoordinates;
            }

            // Get coordinates from OSM using the locality ID
            const locationDetails = await this.getCoordinatesFromOsmId(osmId);

            if (locationDetails) {
                return {
                    latitude: locationDetails.latitude,
                    longitude: locationDetails.longitude
                };
            }

            return defaultCoordinates;
        } catch (error) {
            console.warn('Failed to get user location from API, using default coordinates:', error);
            return defaultCoordinates;
        }
    }

    /**
     * Get coordinates from OSM ID using Nominatim lookup API
     */
    private async getCoordinatesFromOsmId(osmId: number): Promise<{ latitude: number; longitude: number } | null> {
        try {
            const url = `https://nominatim.openstreetmap.org/lookup?osm_ids=N${osmId},W${osmId},R${osmId}&format=json`;
            const response = await fetch(url);
            const data = await response.json();

            if (data && data.length > 0) {
                return {
                    latitude: parseFloat(data[0].lat),
                    longitude: parseFloat(data[0].lon)
                };
            }

            return null;
        } catch (error) {
            console.error('Error fetching coordinates from OSM ID:', error);
            return null;
        }
    }
}

