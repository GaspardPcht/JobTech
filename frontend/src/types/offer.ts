export interface Tech {
  id: number;
  name: string;
}

export interface Offer {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string;
  salary_min: number | null;
  salary_max: number | null;
  contract_type: string | null;
  remote: boolean;
  url: string;
  posted_at: string;
  created_at: string;
  updated_at: string;
  techs: Tech[];
}

export interface OfferFilters {
  keywords?: string;
  location?: string;
  contract_type?: string;
  remote?: boolean;
  sources?: 'all' | 'adzuna' | 'pole-emploi';
  limit?: number;
  sort_by?: 'date' | 'relevance';
  page?: number;
  tech_only?: boolean;
}
