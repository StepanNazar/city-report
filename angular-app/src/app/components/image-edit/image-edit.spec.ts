import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ImageEdit } from './image-edit';

describe('ImageEdit', () => {
    let component: ImageEdit;
    let fixture: ComponentFixture<ImageEdit>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [ImageEdit]
        })
            .compileComponents();

        fixture = TestBed.createComponent(ImageEdit);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});

