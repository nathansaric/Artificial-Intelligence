; =============================
; Student Names: Hannah Larsen, Nathan Saric
; Group ID: Group 13
; Date: March 9th, 2022
; =============================
(define (problem p3-dungeon)
  (:domain Dungeon)

  ; Naming convention:
  ; - loc{i}{j} refers to the location at the i'th column and j'th row (starting in top left corner)
  ; - c{i}{j}{h}{k} refers to the corridor connecting loc{i}{j} and loc{h}{k}
  (:objects
    loc34 loc45 loc12 loc22 loc32 loc33 loc25 loc13 loc21 loc14 loc35 loc24 loc44 loc23 loc43 - location
    c2122 c1222 c2232 c1213 c1223 c2223 c3223 c3233 c1323 c2333 c1314 c2314 c2324 c2334 c3334 c1424 c2434 c2425 c2535 c3545 c4544 c4443 - corridor
    key1 key2 key3 key4 key5 key6 - key
  )

(:init
    ; Hero location and carrying status
    (hero-at loc21)
    (hero-empty)

    ; Location <> Corridor Connections
    (loc-connected-to-cor loc12 c1213)
    (loc-connected-to-cor loc12 c1222)
    (loc-connected-to-cor loc12 c1223)

    (loc-connected-to-cor loc13 c1213)
    (loc-connected-to-cor loc13 c1314)
    (loc-connected-to-cor loc13 c1323)

    (loc-connected-to-cor loc14 c1314)
    (loc-connected-to-cor loc14 c1424)
    (loc-connected-to-cor loc14 c2314)

    (loc-connected-to-cor loc21 c2122)

    (loc-connected-to-cor loc22 c1222)
    (loc-connected-to-cor loc22 c2122)
    (loc-connected-to-cor loc22 c2223)
    (loc-connected-to-cor loc22 c2232)

    (loc-connected-to-cor loc23 c1223)
    (loc-connected-to-cor loc23 c1323)
    (loc-connected-to-cor loc23 c2223)
    (loc-connected-to-cor loc23 c2314)
    (loc-connected-to-cor loc23 c2324)
    (loc-connected-to-cor loc23 c2333)
    (loc-connected-to-cor loc23 c2334)
    (loc-connected-to-cor loc23 c3223)

    (loc-connected-to-cor loc24 c1424)
    (loc-connected-to-cor loc24 c2324)
    (loc-connected-to-cor loc24 c2425)
    (loc-connected-to-cor loc24 c2434)

    (loc-connected-to-cor loc25 c2425)
    (loc-connected-to-cor loc25 c2535)

    (loc-connected-to-cor loc32 c2232)
    (loc-connected-to-cor loc32 c3223)
    (loc-connected-to-cor loc32 c3233)

    (loc-connected-to-cor loc33 c2333)
    (loc-connected-to-cor loc33 c3233)
    (loc-connected-to-cor loc33 c3334)

    (loc-connected-to-cor loc34 c2334)
    (loc-connected-to-cor loc34 c2434)
    (loc-connected-to-cor loc34 c3334)

    (loc-connected-to-cor loc35 c2535)
    (loc-connected-to-cor loc35 c3545)

    (loc-connected-to-cor loc43 c4443)

    (loc-connected-to-cor loc44 c4443)
    (loc-connected-to-cor loc44 c4544)

    (loc-connected-to-cor loc45 c3545)
    (loc-connected-to-cor loc45 c4544)

    ; Key locations
    (loc-has-key loc21 key1)
    (loc-has-key loc23 key2)
    (loc-has-key loc23 key3)
    (loc-has-key loc23 key4)
    (loc-has-key loc23 key5)
    (loc-has-key loc44 key6)

    ; Unlocked corridors
    (cor-unlocked c1213)
    (cor-unlocked c1222)
    (cor-unlocked c1314)
    (cor-unlocked c1424)
    (cor-unlocked c2122)
    (cor-unlocked c2232)
    (cor-unlocked c2434)
    (cor-unlocked c3233)
    (cor-unlocked c3334)

    ; Locked corridors
    (cor-locked c1223 red)
    (cor-locked c1323 red)
    (cor-locked c2223 red)
    (cor-locked c2314 red)
    (cor-locked c2324 red)
    (cor-locked c2333 red)
    (cor-locked c2334 red)
    (cor-locked c2425 purple)
    (cor-locked c2535 green)
    (cor-locked c3223 red)
    (cor-locked c3545 purple)
    (cor-locked c4443 rainbow)
    (cor-locked c4544 green)

    ; Risky corridors
    (cor-risky c1223)
    (cor-risky c1323)
    (cor-risky c2223)
    (cor-risky c2314)
    (cor-risky c2324)
    (cor-risky c2333)
    (cor-risky c2334)
    (cor-risky c3223)

    ; Key colours
    (key-colour key1 red)
    (key-colour key2 purple)
    (key-colour key3 green)
    (key-colour key4 purple)
    (key-colour key5 green)
    (key-colour key6 rainbow)

    ; Key usage properties (one use, two use, etc)
    (key-one-use key2)
    (key-one-use key3)
    (key-one-use key4)
    (key-one-use key5)
    (key-one-use key6)
  )

  (:goal
    (and
      (hero-at loc43)
    )
  )
)