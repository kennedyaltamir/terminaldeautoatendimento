import { getToken } from "./auth";
import { Employee } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function authenticatedFetch(endpoint: string, options: RequestInit = {}) {
  const token = getToken();
  const headers: any = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, { ...options, headers });

  if (!response.ok) {
    const error = new Error("Erro na requisição");
    (error as any).status = response.status;
    throw error;
  }

  return response;
}

export async function getEmployees(slug: string): Promise<Employee[]> {
  const res = await authenticatedFetch("/admin/employees");
  return res.json();
}

export async function createEmployee(slug: string, data: any): Promise<Employee> {
  const res = await authenticatedFetch("/admin/employees", {
    method: "POST",
    body: JSON.stringify(data),
  });
  return res.json();
}

/**
 * 🛡️ FIX: Alterado de PUT para PATCH para alinhar com o backend FastAPI.
 * O erro 405 ocorria porque o servidor não aceita PUT nesta rota.
 */
export async function updateEmployee(slug: string, id: number, data: any): Promise<Employee> {
  const res = await authenticatedFetch(`/admin/employees/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function deleteEmployee(slug: string, id: number): Promise<void> {
  await authenticatedFetch(`/admin/employees/${id}`, {
    method: "DELETE",
  });
}