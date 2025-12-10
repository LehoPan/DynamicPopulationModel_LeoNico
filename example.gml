graph [
  directed 0

  # --- Community A (0-6) ---

  node [ id 0 label 0 ]
  node [ id 1 label 1 ]
  node [ id 2 label 2 ]
  node [ id 3 label 3 ]
  node [ id 4 label 4 ]
  node [ id 5 label 5 ]
  node [ id 6 label 6 ]

  # Triangle 0-1-2
  edge [ source 0 target 1 ]
  edge [ source 1 target 2 ]
  edge [ source 2 target 0 ]

  # Cycle 2-3-4-5-2
  edge [ source 2 target 3 ]
  edge [ source 3 target 4 ]
  edge [ source 4 target 5 ]
  edge [ source 5 target 2 ]

  # Extra connections to 6 (to make A denser)
  edge [ source 3 target 6 ]
  edge [ source 4 target 6 ]
  edge [ source 5 target 6 ]

  # --- Community B (7-13) ---

  node [ id 7  label 7  ]
  node [ id 8  label 8  ]
  node [ id 9  label 9  ]
  node [ id 10 label 10 ]
  node [ id 11 label 11 ]
  node [ id 12 label 12 ]
  node [ id 13 label 13 ]

  # Triangle 7-8-9
  edge [ source 7 target 8 ]
  edge [ source 8 target 9 ]
  edge [ source 9 target 7 ]

  # 8,9,10 tightly connected
  edge [ source 8  target 10 ]
  edge [ source 9  target 10 ]

  # Chain/loop 10-11-12-13-10
  edge [ source 10 target 11 ]
  edge [ source 11 target 12 ]
  edge [ source 12 target 13 ]
  edge [ source 13 target 10 ]

  # Extra internal edge to make B denser
  edge [ source 8 target 11 ]
  edge [ source 9 target 12 ]

  # --- Single bridge between communities ---

  # Only connection A <-> B is 2 -- 7
  # Node 7 has neighbors: 8, 9, 10, 2  (degree 4)
  edge [ source 2 target 7 ]
]
