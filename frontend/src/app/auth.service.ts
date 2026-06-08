import { inject, Injectable } from '@angular/core';
import { Auth, GoogleAuthProvider, signInWithPopup, signOut, user } from '@angular/fire/auth';
import { doc, Firestore, getDoc, setDoc, serverTimestamp } from '@angular/fire/firestore';
import { from, Observable, switchMap, of } from 'rxjs';

export interface AppUser {
  uid: string;
  name: string | null;
  email: string | null;
  photoURL: string | null;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private auth = inject(Auth);
  private firestore = inject(Firestore);

  /** Emits the current user or null when signed out. */
  user$: Observable<AppUser | null> = user(this.auth).pipe(
    switchMap(firebaseUser => {
      if (!firebaseUser) return of(null);
      return of({
        uid: firebaseUser.uid,
        name: firebaseUser.displayName,
        email: firebaseUser.email,
        photoURL: firebaseUser.photoURL,
      });
    })
  );

  async signInWithGoogle(): Promise<void> {
    const provider = new GoogleAuthProvider();
    const credential = await signInWithPopup(this.auth, provider);
    await this._ensureUserDoc(credential.user);
  }

  signOut(): Promise<void> {
    return signOut(this.auth);
  }

  private async _ensureUserDoc(firebaseUser: import('@angular/fire/auth').User): Promise<void> {
    const ref = doc(this.firestore, 'users', firebaseUser.uid);
    const snap = await getDoc(ref);
    if (!snap.exists()) {
      await setDoc(ref, {
        uid: firebaseUser.uid,
        name: firebaseUser.displayName,
        email: firebaseUser.email,
        photoURL: firebaseUser.photoURL,
        createdAt: serverTimestamp(),
      });
    }
  }
}
