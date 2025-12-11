import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ImageLightbox } from './image-lightbox';

describe('ImageLightbox', () => {
    let component: ImageLightbox;
    let fixture: ComponentFixture<ImageLightbox>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [ImageLightbox]
        })
            .compileComponents();

        fixture = TestBed.createComponent(ImageLightbox);
        component = fixture.componentInstance;
        fixture.componentRef.setInput('images', [
            { id: '1', url: 'test1.jpg' },
            { id: '2', url: 'test2.jpg' }
        ]);
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});

