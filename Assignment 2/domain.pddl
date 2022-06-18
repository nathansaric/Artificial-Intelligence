; =============================
; Student Names: Hannah Larsen, Nathan Saric
; Group ID: Group 13
; Date: March 9th, 2022
; =============================
(define (domain Dungeon)

    (:requirements
        :typing
        :negative-preconditions
        :conditional-effects
    )

    ; Do not modify the types
    (:types
        location colour key corridor
    )

    ; Do not modify the constants
    (:constants
        red yellow green purple rainbow - colour
    )

    ; You may introduce whatever predicates you would like to use
    (:predicates

        ; Hero predicates
        (hero-at ?loc - location)
        (hero-empty)
        (hero-holding ?k - key)

        ; Corridor predicates
        (cor-risky ?cor - corridor)
        (cor-unlocked ?cor - corridor)
        (cor-locked ?cor - corridor ?col - colour)

        ; Location predicates
        (loc-connected-to-cor ?loc - location ?cor - corridor)
        (loc-has-key ?loc - location ?k - key)

        ; Key predicates
        (key-colour ?k - key ?col - colour)
        (key-one-use ?k - key)
        (key-two-use ?k - key)
        (key-used-up ?k - key)
    )

    ; IMPORTANT: You should not change/add/remove the action names or parameters

    ;Hero can move if the
    ;    - hero is at current location ?from,
    ;    - hero wants to move to location ?to,
    ;    - corridor ?cor exists between the ?from and ?to locations
    ;    - there isn't a locked door in corridor ?cor
    ;Effects move the hero, and collapse the corridor if it's "risky"
    (:action move

        :parameters (?from ?to - location ?cor - corridor)

        :precondition (and 
        (hero-at ?from) 
        (not (hero-at ?to))
        (loc-connected-to-cor ?from ?cor)
        (loc-connected-to-cor ?to ?cor)
        (cor-unlocked ?cor)
        )

        :effect (and
        (hero-at ?to)
        (not (hero-at ?from))
        (when (cor-risky ?cor) (and (not (loc-connected-to-cor ?from ?cor)) (not (loc-connected-to-cor ?to ?cor)))))
    )

    ;Hero can pick up a key if the
    ;    - hero is at current location ?loc,
    ;    - there is a key ?k at location ?loc,
    ;    - the hero's arm is free,
    ;Effect will have the hero holding the key and their arm no longer being free
    (:action pick-up

        :parameters (?loc - location ?k - key)

        :precondition (and
        (hero-at ?loc)
        (loc-has-key ?loc ?k)
        (hero-empty)
        )

        :effect (and
        (hero-holding ?k)
        (not(loc-has-key ?loc ?k))
        (not(hero-empty))
        )
    )

    ;Hero can drop a key if the
    ;    - hero is holding a key ?k,
    ;    - the hero is at location ?loc
    ;Effect will be that the hero is no longer holding the key
    (:action drop

        :parameters (?loc - location ?k - key)

        :precondition (and
        (hero-at ?loc)
        (hero-holding ?k)
        (not(hero-empty))
        )

        :effect (and
        (loc-has-key ?loc ?k)
        (not(hero-holding ?k))
        (hero-empty)
        )
    )

    ;Hero can use a key for a corridor if
    ;    - the hero is holding a key ?k,
    ;    - the key still has some uses left,
    ;    - the corridor ?cor is locked with colour ?col,
    ;    - the key ?k is if the right colour ?col,
    ;    - the hero is at location ?loc
    ;    - the corridor is connected to the location ?loc
    ;Effect will be that the corridor is unlocked and the key usage will be updated if necessary
    (:action unlock

        :parameters (?loc - location ?cor - corridor ?col - colour ?k - key)

        :precondition (and
        (hero-at ?loc)
        (hero-holding ?k)
        (cor-locked ?cor ?col)
        (loc-connected-to-cor ?loc ?cor)
        (key-colour ?k ?col)
        (not(key-used-up ?k))
        )

        :effect (and
        (cor-unlocked ?cor)
        (when (key-two-use ?k) (key-one-use ?k))
        (when (key-one-use ?k) (key-used-up ?k))
        )
    )
)
