**Table 1: "public""CUSTOMER"**

- index: bigint
- C_CUSTKEY: bigint
- C_NATIONKEY: bigint
- C_ACCTBAL: double precision
- C_MKTSEGMENT: text
- C_PHONE: text
- C_COMMENT: text
- C_NAME: text
- C_ADDRESS: text

**Table 2: "public""LINEITEM"**

- index: bigint
- L_ORDERKEY: bigint
- L_PARTKEY: bigint
- L_SUPPKEY: bigint
- L_LINENUMBER: bigint
- L_QUANTITY: double precision
- L_EXTENDEDPRICE: double precision
- L_DISCOUNT: double precision
- L_TAX: double precision
- L_RETURNFLAG: text
- L_LINESTATUS: text
- L_SHIPDATE: text
- L_COMMITDATE: text
- L_RECEIPTDATE: text
- L_SHIPINSTRUCT: text
- L_SHIPMODE: text
- L_COMMENT: text

**Table 3: "public""NATION"**

- index: bigint
- N_NATIONKEY: bigint
- N_REGIONKEY: bigint
- N_NAME: text
- N_COMMENT: text

**Table 4: "public""ORDERS"**

- O_CUSTKEY: bigint
- O_ORDERKEY: bigint
- O_TOTALPRICE: double precision
- O_SHIPPRIORITY: bigint
- index: bigint
- O_COMMENT: text
- O_ORDERSTATUS: text
- O_ORDERDATE: text
- O_ORDERPRIORITY: text
- O_CLERK: text

**Table 5: "public""PART"**

- P_SIZE: bigint
- P_PARTKEY: bigint
- P_RETAILPRICE: double precision
- index: bigint
- P_TYPE: text
- P_CONTAINER: text
- P_COMMENT: text
- P_NAME: text
- P_MFGR: text
- P_BRAND: text

**Table 6: "public""PARTSUPP"**

- index: bigint
- PS_PARTKEY: bigint
- PS_SUPPKEY: bigint
- PS_AVAILQTY: bigint
- PS_SUPPLYCOST: double precision
- PS_COMMENT: text

**Table 7: "public""REGION"**

- index: bigint
- R_REGIONKEY: bigint
- R_NAME: text
- R_COMMENT: text

**Table 8: "public""SUPPLIER"**

- index: bigint
- S_SUPPKEY: bigint
- S_NATIONKEY: bigint
- S_ACCTBAL: double precision
- S_COMMENT: text
- S_PHONE: text
- S_NAME: text
- S_ADDRESS: text

