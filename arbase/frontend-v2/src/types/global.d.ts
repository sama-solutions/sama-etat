declare module '../../ar-engine-v2' {
  export interface ARExperience {
    id: string;
    qrCode: string;
    content: any[];
    settings: any;
    [key: string]: any;
  }
  
  export const ARSupport: {
    checkFullSupport(): Promise<{
      webxr: boolean;
      camera: boolean;
      webgl: boolean;
      webworker: boolean;
      overall: boolean;
    }>;
  };
}