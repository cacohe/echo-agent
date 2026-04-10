import { API_BASE_URL } from "./constants";
import type { JournalRecord, Insight, Reminder } from "./types";

export interface RecordCreate {
  content: string;
  type: "voice" | "text";
  mood?: "happy" | "neutral" | "low" | "angry";
  context?: string;
}

export interface RecordResponse {
  id: string;
  content: string;
  type: "voice" | "text";
  mood?: "happy" | "neutral" | "low" | "angry";
  context?: string;
  created_at: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${path}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async createRecord(data: RecordCreate): Promise<{
    record: RecordResponse;
    insights: Insight[];
  }> {
    return this.request("/api/records", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async getRecords(limit: number = 50, offset: number = 0): Promise<RecordResponse[]> {
    return this.request(`/api/records?limit=${limit}&offset=${offset}`);
  }

  async getRecord(id: string): Promise<RecordResponse> {
    return this.request(`/api/records/${id}`);
  }

  async getWeeklyReport(period?: string): Promise<any> {
    const path = period ? `/api/insights/weekly?period=${period}` : "/api/insights/weekly";
    return this.request(path);
  }

  async getReminders(): Promise<Reminder[]> {
    return this.request("/api/insights/reminders");
  }

  async createReminder(data: Omit<Reminder, "id">): Promise<Reminder> {
    return this.request("/api/insights/reminders", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new ApiClient();
