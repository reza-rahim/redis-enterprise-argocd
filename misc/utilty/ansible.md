
```
openshift-login/
├── group_vars/
│   └── all/
│       ├── vars.yml          # non-secret vars
│       └── vault.yml         # secrets (vault-encrypted)
├── login.yml
```
group_vars/all/vars.yml

```
# OpenShift API endpoint (no trailing slash)
oc_api_url: "https://api.mycluster.example.com:6443"

# User to login as
oc_username: "myuser"

# Optional: project/namespace to switch to after login
oc_project: "my-namespace"

# Where to store kubeconfig for this login
kubeconfig_path: "{{ ansible_env.HOME }}/.kube/oc-login.kubeconfig"

# Set to true if your cluster uses a self-signed cert and you want to skip TLS verify
oc_insecure_skip_tls_verify: false

```

group_vars/all/vault.yml (will be encrypted by Vault)
```
oc_password: "REPLACE_ME"   # will be encrypted; see step 4
```

login.yml
```
- name: Login to OpenShift with oc using a vaulted password
  hosts: localhost
  gather_facts: false

  vars_files:
    - group_vars/all/vars.yml
    - group_vars/all/vault.yml

  pre_tasks:
    - name: Ensure oc CLI is available
      ansible.builtin.command: oc version --client
      register: oc_cli_check
      changed_when: false
      failed_when: oc_cli_check.rc != 0

    - name: Ensure kubeconfig directory exists
      ansible.builtin.file:
        path: "{{ kubeconfig_path | dirname }}"
        state: directory
        mode: "0700"

  tasks:
    - name: Check current oc identity (if already logged in for this kubeconfig)
      ansible.builtin.command: >
        oc whoami --kubeconfig {{ kubeconfig_path }}
      register: oc_whoami
      changed_when: false
      failed_when: false

    - name: Decide if login is needed
      ansible.builtin.set_fact:
        oc_login_needed: "{{ (oc_whoami.rc != 0) or (oc_whoami.stdout | default('') != oc_username) }}"

    - name: oc login (password kept secret)
      ansible.builtin.command: >
        oc login {{ oc_api_url }}
        -u {{ oc_username }}
        -p {{ oc_password }}
        --kubeconfig {{ kubeconfig_path }}
        {% if oc_insecure_skip_tls_verify %} --insecure-skip-tls-verify=true {% endif %}
      no_log: true
      when: oc_login_needed

    - name: Switch to desired project (optional)
      ansible.builtin.command: >
        oc project {{ oc_project }} --kubeconfig {{ kubeconfig_path }}
      when: oc_project is defined and oc_project|length > 0
      register: oc_project_switch
      changed_when: "'now using project' in (oc_project_switch.stdout | lower | default(''))"
```

4) Create the vaulted secrets file

```
ansible-vault encrypt_string 'SuperSecretP@ss!' --name 'oc_password' \
  > group_vars/all/vault.yml

ansible-vault encrypt_string 'SuperSecretP@ss!' --name 'oc_password' \
  > group_vars/all/vault.yml

ansible-playbook login.yml --ask-vault-pass

ansible-playbook login.yml --vault-password-file ~/.vault_pass.txt

```

```
- name: Create a temporary render directory
      ansible.builtin.tempfile:
        state: directory
        prefix: oc-render-
      register: tempdir

    - name: Set path for rendered manifest
      ansible.builtin.set_fact:
        render_path: "{{ tempdir.path }}/{{ app_name }}.deployment.yaml"

    - name: Render Kubernetes/OpenShift deployment from template
      ansible.builtin.template:
        src: "templates/deployment.yaml.j2"
        dest: "{{ render_path }}"
        mode: "0600"

    - name: Apply rendered manifest with oc
      ansible.builtin.command: >
        oc apply -f {{ render_path }}
        --kubeconfig {{ kubeconfig_path }}
        {% if oc_insecure_skip_tls_verify %} --insecure-skip-tls-verify=true {% endif %}
      register: oc_apply
      changed_when: >
        (' created' in oc_apply.stdout) or
        (' configured' in oc_apply.stdout) or
        ('patched' in oc_apply.stdout)
      failed_when: oc_apply.rc != 0

    - name: Wait for rollout to complete
      ansible.builtin.command: >
        oc rollout status deployment/{{ app_name }}
        --namespace {{ oc_namespace }}
        --kubeconfig {{ kubeconfig_path }}
        --timeout=120s
      register: oc_rollout
      changed_when: false
      failed_when: oc_rollout.rc != 0

  post_tasks:
    - name: Remove temporary render directory
      ansible.builtin.file:
        path: "{{ tempdir.path }}"
        state: absent
```

