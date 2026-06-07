import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ProfileService } from './profile.service';
import { Profile } from './profile.model';

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private profileService = inject(ProfileService);
  private http = inject(HttpClient);

  profile = signal<Profile | null>(null);
  loading = signal(false);
  error = signal(false);
  copiedField = signal<string | null>(null);

  bulkCount = 100;
  bulkDownloading = signal(false);
  bulkError = signal(false);

  ngOnInit() {
    this.refresh();
  }

  refresh() {
    this.loading.set(true);
    this.error.set(false);
    this.profileService.getProfile().subscribe({
      next: (p) => { this.profile.set(p); this.loading.set(false); },
      error: () => { this.error.set(true); this.loading.set(false); }
    });
  }

  copy(value: string, field: string) {
    navigator.clipboard.writeText(value).then(() => {
      this.copiedField.set(field);
      setTimeout(() => this.copiedField.set(null), 1800);
    });
  }

  downloadProfile() {
    const p = this.profile();
    if (!p) return;
    const blob = new Blob([JSON.stringify(p, null, 2)], { type: 'application/json' });
    this._triggerDownload(blob, `profile_${p.first_name}_${p.last_name}.json`);
  }

  downloadBulkCSV() {
    const count = Math.max(1, Math.min(5000, this.bulkCount || 10));
    this.bulkDownloading.set(true);
    this.bulkError.set(false);
    this.http.get(`/api/employees?count=${count}`, { responseType: 'blob' }).subscribe({
      next: (blob) => {
        this._triggerDownload(blob, `employees_${count}.csv`);
        this.bulkDownloading.set(false);
      },
      error: () => { this.bulkError.set(true); this.bulkDownloading.set(false); }
    });
  }

  private _triggerDownload(blob: Blob, filename: string) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }
}
