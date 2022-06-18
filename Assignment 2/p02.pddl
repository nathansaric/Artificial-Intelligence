; =============================
; Student Names: Hannah Larsen, Nathan Saric
; Group ID: Group 13
; Date: March 9, 2022
; =============================
(define (problem p2-dungeon)
  (:domain Dungeon)

  ; Naming convention:
  ; - loc{i}{j} refers to the location at the i'th column and j'th row (starting in top left corner)
  ; - c{i}{j}{h}{k} refers to the corridor connecting loc{i}{j} and loc{h}{k}
  (:objects
    loc21 loc12 loc22 loc32 loc42 loc23 - location
    key1 key2 key3 key4 - key
    c2122 c1222 c2232 c3242 c2223 - corridor
  )

  (:init
    ; Hero location and carrying status
    (hero-at loc22)
    (hero-empty)

    ; Location <> Corridor Connections
    (loc-connected-to-cor loc12 c1222)

    (loc-connected-to-cor loc21 c2122)

    (loc-connected-to-cor loc22 c1222)
    (loc-connected-to-cor loc22 c2122)
    (loc-connected-to-cor loc22 c2223)
    (loc-connected-to-cor loc22 c2232)

    (loc-connected-to-cor loc23 c2223)

    (loc-connected-to-cor loc32 c2232)
    (loc-connected-to-cor loc32 c3242)

    (loc-connected-to-cor loc42 c3242)

    ; Key locations
    (loc-has-key loc22 key1)
    (loc-has-key loc21 key2)
    (loc-has-key loc23 key3)
    (loc-has-key loc12 key4)

    ; Locked corridors
    (cor-locked c1222 yellow)
    (cor-locked c2122 purple)
    (cor-locked c2223 green)
    (cor-locked c2232 yellow)
    (cor-locked c3242 rainbow)

    ; Key colours
    (key-colour key1 purple)
    (key-colour key2 green)
    (key-colour key3 yellow)
    (key-colour key4 rainbow)

    ; Key usage properties (one use, two use, etc)
    (key-one-use key1)
    (key-one-use key2)
    (key-two-use key3)
    (key-one-use key4)
  )

  (:goal
    (and
      (hero-at loc42)
    )
  )
)
