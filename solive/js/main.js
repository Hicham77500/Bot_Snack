import { gererChange, gererClic, gererSaisie } from "./actions.js";
import { getState, subscribe } from "./store.js";
import { render } from "./views.js";

const root = document.querySelector("#root");

function lireRoute() {
  const parts = (location.hash || "#/").replace(/^#/, "").split("/").filter(Boolean);
  if (parts[0] !== "app") return { page: "landing" };
  return { page: parts[1] ?? "dashboard", id: parts[2] ?? null };
}

function dessiner() {
  root.innerHTML = render(getState(), lireRoute());
}

document.body.addEventListener("click", (event) => {
  const bouton = event.target.closest("[data-action]");
  if (!bouton || !root.contains(bouton)) return;
  gererClic(bouton);
});

document.body.addEventListener("input", (event) => {
  if (!(event.target instanceof HTMLElement) || !event.target.dataset.bind) return;
  if (event.target.dataset.bind === "pointage") return;
  gererSaisie(event.target);
});

document.body.addEventListener("change", (event) => {
  if (!(event.target instanceof HTMLElement) || !event.target.dataset.bind) return;
  if (event.target.dataset.bind === "avancement" || event.target.dataset.bind === "ligne" || event.target.dataset.bind === "frais") return;
  gererChange(event.target);
});

window.addEventListener("hashchange", dessiner);
subscribe(dessiner);
dessiner();
