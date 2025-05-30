// Types pour les technologies et tendances technologiques

export interface Tech {
  id: number;
  name: string;
  category: string;
  description?: string;
}

export interface TechWithStats extends Tech {
  offer_count: number;
}

export interface TechTrend {
  name: string;
  category: string;
  count: number;
  percentage: number;
}
