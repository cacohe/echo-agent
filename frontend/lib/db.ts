import { openDB, DBSchema, IDBPDatabase } from "idb";
import type { JournalRecord, Insight, Reminder } from "./types";

interface EchoDB extends DBSchema {
  records: {
    key: string;
    value: JournalRecord;
    indexes: { "by-date": string };
  };
  insights: {
    key: string;
    value: Insight;
    indexes: { "by-record": string };
  };
  reminders: {
    key: string;
    value: Reminder;
  };
}

const DB_NAME = "echo_db";
const DB_VERSION = 1;

let dbPromise: Promise<IDBPDatabase<EchoDB>> | null = null;

export function getDB(): Promise<IDBPDatabase<EchoDB>> {
  if (!dbPromise) {
    dbPromise = openDB<EchoDB>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains("records")) {
          const recordStore = db.createObjectStore("records", { keyPath: "id" });
          recordStore.createIndex("by-date", "created_at");
        }
        if (!db.objectStoreNames.contains("insights")) {
          const insightStore = db.createObjectStore("insights", { keyPath: "id" });
          insightStore.createIndex("by-record", "record_id");
        }
        if (!db.objectStoreNames.contains("reminders")) {
          db.createObjectStore("reminders", { keyPath: "id" });
        }
      },
    });
  }
  return dbPromise;
}

export async function addRecord(record: JournalRecord): Promise<void> {
  const db = await getDB();
  await db.add("records", record);
}

export async function getRecord(id: string): Promise<JournalRecord | undefined> {
  const db = await getDB();
  return db.get("records", id);
}

export async function getAllRecords(): Promise<JournalRecord[]> {
  const db = await getDB();
  const records = await db.getAllFromIndex("records", "by-date");
  return records.reverse();
}

export async function getRecentRecords(limit: number = 20): Promise<JournalRecord[]> {
  const db = await getDB();
  const records = await db.getAllFromIndex("records", "by-date");
  return records.reverse().slice(0, limit);
}

export async function deleteRecord(id: string): Promise<void> {
  const db = await getDB();
  await db.delete("records", id);
}

export async function addInsight(insight: Insight): Promise<void> {
  const db = await getDB();
  await db.add("insights", insight);
}

export async function getInsightsByRecord(recordId: string): Promise<Insight[]> {
  const db = await getDB();
  return db.getAllFromIndex("insights", "by-record", recordId);
}

export async function getAllInsights(): Promise<Insight[]> {
  const db = await getDB();
  return db.getAll("insights");
}

export async function addReminder(reminder: Reminder): Promise<void> {
  const db = await getDB();
  await db.add("reminders", reminder);
}

export async function getActiveReminders(): Promise<Reminder[]> {
  const db = await getDB();
  const all = await db.getAll("reminders");
  return all.filter((r) => r.active);
}

export async function updateReminder(reminder: Reminder): Promise<void> {
  const db = await getDB();
  await db.put("reminders", reminder);
}
