import { Component, input, output, signal, computed, ChangeDetectionStrategy } from '@angular/core';
import { ImageResponse } from '../../services/posts.service';

@Component({
    selector: 'app-image-lightbox',
    imports: [],
    templateUrl: './image-lightbox.html',
    styleUrl: './image-lightbox.scss',
    changeDetection: ChangeDetectionStrategy.OnPush,
    host: {
        '(document:keydown.escape)': 'close()',
        '(document:keydown.arrowLeft)': 'previous()',
        '(document:keydown.arrowRight)': 'next()'
    }
})
export class ImageLightbox {
    readonly images = input.required<ImageResponse[]>();
    readonly initialIndex = input<number>(0);
    readonly closeClicked = output<void>();

    readonly currentIndex = signal<number>(0);
    readonly currentImage = computed(() => {
        const images = this.images();
        const index = this.currentIndex();
        return images[index];
    });

    readonly hasPrevious = computed(() => this.currentIndex() > 0);
    readonly hasNext = computed(() => this.currentIndex() < this.images().length - 1);

    constructor() {
        // Set initial index when component is created
        setTimeout(() => {
            this.currentIndex.set(this.initialIndex());
        });
    }

    previous() {
        if (this.hasPrevious()) {
            this.currentIndex.update(index => index - 1);
        }
    }

    next() {
        if (this.hasNext()) {
            this.currentIndex.update(index => index + 1);
        }
    }

    close() {
        this.closeClicked.emit();
    }

    onBackdropClick(event: MouseEvent) {
        if (event.target === event.currentTarget) {
            this.close();
        }
    }
}

