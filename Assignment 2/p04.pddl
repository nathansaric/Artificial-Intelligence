; =============================
; Student Names: Hannah Larsen, Nathan Saric
; Group ID: Group 13
; Date: March 9th, 2022
; =============================
(define (problem p4-dungeon)
  (:domain Dungeon)

  ; Come up with your own problem instance (see assignment for details)
  ; NOTE: You _may_ use new objects for this problem only.

  ; Naming convention:
  ; - loc{i}{j} refers to the location at the i'th column and j'th row (starting in top left corner)
  ; - c{i}{j}{h}{k} refers to the corridor connecting loc{i}{j} and loc{h}{k}
(:objects
    loc11 loc12 loc13 loc21 loc22 loc23 loc31 loc32 loc33 - location
    key1 key2 key3 key4 key5 - key
    c1112 c1121 c1213 c1323 c2122 c2332 c2333 c3132 c3233 - corridor
  )

  (:init
    ; Hero location and carrying status
    (hero-at loc11)
    (hero-empty)

    ; Location <> Corridor Connections
    (loc-connected-to-cor loc11 c1112)
    (loc-connected-to-cor loc11 c1121)

    (loc-connected-to-cor loc12 c1112)
    (loc-connected-to-cor loc12 c1213)

    (loc-connected-to-cor loc13 c1213)
    (loc-connected-to-cor loc13 c1323)

    (loc-connected-to-cor loc21 c1121)
    (loc-connected-to-cor loc21 c2122)
    
    (loc-connected-to-cor loc22 c2122)

    (loc-connected-to-cor loc23 c1323)
    (loc-connected-to-cor loc23 c2332)
    (loc-connected-to-cor loc23 c2333)

    (loc-connected-to-cor loc31 c3132)

    (loc-connected-to-cor loc32 c2332)
    (loc-connected-to-cor loc32 c3132)
    (loc-connected-to-cor loc32 c3233)

    (loc-connected-to-cor loc33 c2333)
    (loc-connected-to-cor loc33 c3233)

    ; Key locations
    (loc-has-key loc11 key1)
    (loc-has-key loc11 key2)
    (loc-has-key loc13 key3)
    (loc-has-key loc33 key4)
    (loc-has-key loc31 key5)

    ; Unlocked corridors
    (cor-unlocked c1213)
    (cor-unlocked c1323)

    ; Locked corridors
    (cor-locked c1112 yellow)
    (cor-locked c1121 red)
    (cor-locked c2122 rainbow)
    (cor-locked c2332 green)
    (cor-locked c2333 red)
    (cor-locked c3132 yellow)
    (cor-locked c3233 purple)

    ; Risky corridors
    (cor-risky c1121)
    (cor-risky c2333)

    ; Key colours
    (key-colour key1 red)
    (key-colour key2 yellow)
    (key-colour key3 purple)
    (key-colour key4 green)
    (key-colour key5 rainbow)

    ; Key usage properties (one use, two use, etc)
    (key-two-use key2)
    (key-one-use key3)
    (key-one-use key4)
    (key-one-use key5)
  )

  (:goal
    (and
      (hero-at loc22)
    )
  )
)