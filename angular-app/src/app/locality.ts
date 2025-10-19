export interface Locality {
  id: number;
  name: string;
  countryId: number;
  stateId: number;
  users: number;
  posts: number;
  approvedSolutions: number;
  createdAt: Date;
}
