"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { User, UserRole } from "./types";
import { apiService } from "./api";

interface AuthContextType {
  user: User | null;
  role: UserRole;
  setRole: (role: UserRole) => void;
  token: string | null;
  login: (token: string, user: User) => void;
  logout: () => void;
  selectedDistrict: number | undefined;
  setSelectedDistrict: (districtCode: number | undefined) => void;
}

const defaultUser: User = {
  id: 1,
  email: "state_admin@karnataka.gov.in",
  full_name: "Dr. R. K. Swamy (State Health Director)",
  role: "STATE_ADMIN",
};

const AuthContext = createContext<AuthContextType>({
  user: defaultUser,
  role: "STATE_ADMIN",
  setRole: () => {},
  token: null,
  login: () => {},
  logout: () => {},
  selectedDistrict: undefined,
  setSelectedDistrict: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(defaultUser);
  const [role, setRoleState] = useState<UserRole>("STATE_ADMIN");
  const [token, setToken] = useState<string | null>(null);
  const [selectedDistrict, setSelectedDistrict] = useState<number | undefined>(undefined);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedRole = localStorage.getItem("role") as UserRole;
    if (savedToken) {
      setToken(savedToken);
      apiService.getMe()
        .then((u) => {
          setUser(u);
          setRoleState(u.role);
          if (u.district_code) setSelectedDistrict(u.district_code);
        })
        .catch(() => {
          // Fallback to default user persona for demo
          setUser(defaultUser);
        });
    } else if (savedRole) {
      setRoleState(savedRole);
    }
  }, []);

  const setRole = (newRole: UserRole) => {
    setRoleState(newRole);
    localStorage.setItem("role", newRole);
    if (user) {
      setUser({
        ...user,
        role: newRole,
        district_code: newRole === "DHO" || newRole === "MMU_COORDINATOR" ? 524 : undefined
      });
      if (newRole === "DHO" || newRole === "MMU_COORDINATOR") {
        setSelectedDistrict(524); // Bagalkote
      } else {
        setSelectedDistrict(undefined); // Karnataka state-wide
      }
    }
  };

  const login = (newToken: string, newUser: User) => {
    setToken(newToken);
    setUser(newUser);
    setRoleState(newUser.role);
    localStorage.setItem("token", newToken);
    localStorage.setItem("role", newUser.role);
    if (newUser.district_code) setSelectedDistrict(newUser.district_code);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("role");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        role,
        setRole,
        token,
        login,
        logout,
        selectedDistrict,
        setSelectedDistrict,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
