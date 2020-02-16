task fake_protein_change_task_1 {
    Float? ram_gb
    Int? local_disk_gb
    Int? num_preemptions

    File MAF
    String ID
    String STUB
    String OPTION
    File? MAFX

    command {
        set -euo pipefail
        ls -latr ${MAF}
        python /opt/src/fake_protein_change.py -m  ${MAF} -i ${ID} -s ${STUB} ${OPTION} -x ${default="" MAFX} 
        ls -latr
    }

    output {
        #** Define outputs here**
        File fpc_maf="${ID}.${STUB}.maf"
        File fpc_snp_maf="${ID}.${STUB}.SNP.maf"
        File fpc_indel_maf="${ID}.${STUB}.INDEL.maf"
    }

    runtime {
        docker : "chipstewart/fake_protein_change_task_1:1"
        memory: "${if defined(ram_gb) then ram_gb else '7'}GB"
        disks : "local-disk ${if defined(local_disk_gb) then local_disk_gb else '20'} HDD"
        preemptible : "${if defined(num_preemptions) then num_preemptions else '0'}"
    }

    meta {
        author : "Chip Stewart"
        email : "stewart@broadinstitute.org"
    }
}

workflow fake_protein_change {

    call fake_protein_change_task_1 

}
