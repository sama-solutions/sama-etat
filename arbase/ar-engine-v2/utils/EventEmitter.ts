/**
 * EventEmitter - Système d'événements simple et performant
 */

export type EventListener = (...args: any[]) => void;

export class EventEmitter {
  private events: Map<string, EventListener[]> = new Map();
  private maxListeners = 10;

  on(event: string, listener: EventListener): this {
    if (!this.events.has(event)) {
      this.events.set(event, []);
    }

    const listeners = this.events.get(event)!;
    
    if (listeners.length >= this.maxListeners) {
      console.warn(`MaxListenersExceededWarning: Possible EventEmitter memory leak detected. ${listeners.length + 1} ${event} listeners added.`);
    }

    listeners.push(listener);
    return this;
  }

  once(event: string, listener: EventListener): this {
    const onceWrapper = (...args: any[]) => {
      this.off(event, onceWrapper);
      listener.apply(this, args);
    };

    return this.on(event, onceWrapper);
  }

  off(event: string, listener?: EventListener): this {
    if (!this.events.has(event)) {
      return this;
    }

    const listeners = this.events.get(event)!;

    if (!listener) {
      // Supprimer tous les listeners pour cet événement
      this.events.delete(event);
    } else {
      // Supprimer un listener spécifique
      const index = listeners.indexOf(listener);
      if (index !== -1) {
        listeners.splice(index, 1);
        
        if (listeners.length === 0) {
          this.events.delete(event);
        }
      }
    }

    return this;
  }

  emit(event: string, ...args: any[]): boolean {
    if (!this.events.has(event)) {
      return false;
    }

    const listeners = this.events.get(event)!.slice(); // Copie pour éviter les modifications pendant l'itération

    listeners.forEach(listener => {
      try {
        listener.apply(this, args);
      } catch (error) {
        console.error(`Error in event listener for '${event}':`, error);
      }
    });

    return true;
  }

  listenerCount(event: string): number {
    return this.events.get(event)?.length || 0;
  }

  eventNames(): string[] {
    return Array.from(this.events.keys());
  }

  setMaxListeners(n: number): this {
    this.maxListeners = n;
    return this;
  }

  getMaxListeners(): number {
    return this.maxListeners;
  }

  removeAllListeners(event?: string): this {
    if (event) {
      this.events.delete(event);
    } else {
      this.events.clear();
    }
    return this;
  }
}