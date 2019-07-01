import { TestBed } from '@angular/core/testing';

import { SitterService } from './sitter.service';

describe('SitterService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: SitterService = TestBed.get(SitterService);
    expect(service).toBeTruthy();
  });
});
