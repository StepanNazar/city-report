import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AIConfig } from './aiconfig';

describe('AIConfig', () => {
  let component: AIConfig;
  let fixture: ComponentFixture<AIConfig>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AIConfig]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AIConfig);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
