#!/usr/bin/env bash
# RETIRADO como bloqueador. Ahora solo AVISA de MI residuo sin commitear.
#
#   bash personal/Arquitecto/guard-commit-si-peer-trabaja.sh
#
# ============================================================================
# POR QUE CAMBIO DE PROPOSITO (2026-08-11)
#
# Este script nacio de un modelo causal FALSO: "commitear mientras un peer
# ejecuta le tira el trabajo". Lei el harness y no es asi:
#
#   Get-ExecOutcomeClass          decide confirmed/transient/definitive
#                                 -> menciones a HEAD: CERO
#
#   Restore-TransientExecResidue  unico sitio que escribe head_changed, y SOLO
#                                 se invoca cuando el exec YA fallo: es una
#                                 limpieza post mortem que se abstiene de
#                                 revertir para no pisar el commit ajeno.
#
# Lo que SI hace fallar a un peer es su propio pre-gate cuando ve el arbol
# sucio (tree dirty / staged residue / cambios ajenos). Es decir: el peligro
# no es commitear, es tener cosas SIN commitear.
#
# Consecuencia: bloquear el commit hasta que el peer estuviera ocioso alargaba
# exactamente el estado que le hace dano. Y con dos crons encadenando trabajo,
# "ocioso" no llega nunca: el 2026-08-11 tuve dos rutinas de ruteo dos horas
# armadas sin poder disparar, y una se comio el limite de tiempo en primer
# plano sin hacer nada.
#
# LECCION QUE ESTE FICHERO EXISTE PARA RECORDAR: cuando corriges un modelo, ve
# a RETIRAR las herramientas construidas sobre el anterior. Anotar la
# correccion no basta; la herramienta vieja te sigue obedeciendo.
# ============================================================================
cd "$(dirname "$0")/../.." || exit 2

mio=$(git status --porcelain -- Area_comun runtime/state scripts .github 2>/dev/null | head -20)

if [ -n "$mio" ]; then
  echo "AVISO -- hay cambios sin commitear en rutas gobernadas:"
  echo "$mio" | sed "s/^/    /"
  echo "  Commitea PRONTO: el arbol sucio es lo que hace abortar a los peers, no tu commit."
else
  echo "arbol gobernado limpio"
fi
exit 0
