import { inject, Injectable } from '@angular/core';
import { Firestore, collection, addDoc, query, orderBy, limit, getDocs, serverTimestamp } from '@angular/fire/firestore';
import { Auth } from '@angular/fire/auth';

export interface DownloadRecord {
  id?: string;
  type: 'profile_json' | 'bulk_csv';
  label: string;
  timestamp: Date;
}

@Injectable({ providedIn: 'root' })
export class HistoryService {
  private firestore = inject(Firestore);
  private auth = inject(Auth);

  async recordDownload(type: 'profile_json' | 'bulk_csv', label: string): Promise<void> {
    const uid = this.auth.currentUser?.uid;
    if (!uid) return;
    const col = collection(this.firestore, 'users', uid, 'downloads');
    await addDoc(col, { type, label, timestamp: serverTimestamp() });
  }

  async getDownloads(): Promise<DownloadRecord[]> {
    const uid = this.auth.currentUser?.uid;
    if (!uid) return [];
    const col = collection(this.firestore, 'users', uid, 'downloads');
    const q = query(col, orderBy('timestamp', 'desc'), limit(50));
    const snap = await getDocs(q);
    return snap.docs.map(d => ({
      id: d.id,
      type: d.data()['type'],
      label: d.data()['label'],
      timestamp: d.data()['timestamp']?.toDate() ?? new Date(),
    }));
  }
}
