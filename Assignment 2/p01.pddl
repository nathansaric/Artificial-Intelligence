; =============================
; Student Names: Hannah Larsen, Nathan Saric
; Group ID: Group 13
; Date: March 9, 2022
; =============================
(define (problem p1-dungeon)
  (:domain Dungeon)

  ; Naming convention:
  ; - loc{i}{j} refers to the location at the i'th column and j'th row (starting in top left corner)
  ; - c{i}{j}{h}{k} refers to the corridor connecting loc{i}{j} and loc{h}{k}
  (:objects
    loc31 loc12 loc22 loc32 loc42 loc23 loc33 loc24 loc34 loc44 - location
    key1 key2 key3 key4 - key
    c3132 c1222 c2232 c3242 c2223 c3233 c2333 c2324 c3334 c2434 c3444 - corridor
  )

  (:init
    ; Hero location and carrying status
    (hero-at loc12)
    (hero-empty)

    ; Location <> Corridor Connections
    (loc-connected-to-cor loc12 c1222)

    (loc-connected-to-cor loc22 c1222)
    (loc-connected-to-cor loc22 c2223)
    (loc-connected-to-cor loc22 c2232)

    (loc-connected-to-cor loc23 c2223)
    (loc-connected-to-cor loc23 c2324)
    (loc-connected-to-cor loc23 c2333)

    (loc-connected-to-cor loc24 c2324)
    (loc-connected-to-cor loc24 c2434)

    (loc-connected-to-cor loc31 c3132)

    (loc-connected-to-cor loc32 c2232)
    (loc-connected-to-cor loc32 c3132)
    (loc-connected-to-cor loc32 c3233)
    (loc-connected-to-cor loc32 c3242)

    (loc-connected-to-cor loc33 c2333)
    (loc-connected-to-cor loc33 c3233)
    (loc-connected-to-cor loc33 c3334)

    (loc-connected-to-cor loc34 c2434)
    (loc-connected-to-cor loc34 c3334)
    (loc-connected-to-cor loc34 c3444)

    (loc-connected-to-cor loc42 c3242)

    (loc-connected-to-cor loc44 c3444)

    ; Key locations
    (loc-has-key loc22 key1)
    (loc-has-key loc24 key2)
    (loc-has-key loc44 key3)
    (loc-has-key loc42 key4)

    ; Unlocked corridors
    (cor-unlocked c1222)
    (cor-unlocked c2223)
    (cor-unlocked c2232)
    (cor-unlocked c2333)
    (cor-unlocked c3233)
    (cor-unlocked c3334)

    ; Locked corridors
    (cor-locked c2324 red)
    (cor-locked c2434 red)
    (cor-locked c3132 rainbow)
    (cor-locked c3242 purple)
    (cor-locked c3444 yellow)

    ; Risky corridors
    (cor-risky c2324)
    (cor-risky c2434)

    ; Key colours
    (key-colour key1 red)
    (key-colour key2 yellow)
    (key-colour key3 purple)
    (key-colour key4 rainbow)

    ; Key usage properties (one use, two use, etc)
    (key-two-use key2)
    (key-one-use key3)
    (key-one-use key4)
  )

  (:goal
    (and
      (hero-at loc31)
    )
  )
)
