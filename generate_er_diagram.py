import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(-0.9, 10.0)
ax.axis('off')
fig.patch.set_facecolor('white')

def draw_table(ax, x, y, w, title, cols):
    row_h = 0.42
    hdr_h = 0.55
    total_h = hdr_h + len(cols) * row_h

    # header
    ax.add_patch(patches.Rectangle((x, y - hdr_h), w, hdr_h,
                 facecolor='#2C3E50', edgecolor='#2C3E50', linewidth=1.5, zorder=2))
    ax.text(x + w/2, y - hdr_h/2, title,
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='white', zorder=3)

    for i, (col, tag) in enumerate(cols):
        ry = y - hdr_h - (i + 1) * row_h
        bg = '#FFF8E1' if tag == 'PK' else '#E3F2FD' if tag == 'FK' else 'white'
        ax.add_patch(patches.Rectangle((x, ry), w, row_h,
                     facecolor=bg, edgecolor='#CCCCCC', linewidth=0.6, zorder=2))

        ax.text(x + 0.18, ry + row_h/2, col,
                ha='left', va='center', fontsize=9, zorder=3,
                color='#2C3E50', fontweight='bold' if tag in ('PK','FK') else 'normal')
        if tag:
            ax.text(x + w - 0.12, ry + row_h/2, tag,
                    ha='right', va='center', fontsize=7,
                    color='#E67E22' if tag == 'PK' else '#2980B9' if tag == 'FK' else '#27AE60',
                    fontweight='bold', zorder=3)

    # border
    ax.add_patch(patches.Rectangle((x, y - total_h), w, total_h,
                 facecolor='none', edgecolor='#2C3E50', linewidth=1.8, zorder=4))
    return y - total_h  # bottom y

# Row/header heights (must match draw_table)
ROW_H = 0.42
HDR_H = 0.55

# ── USERS (left) ─────────────────────────────────────────────────
users = [
    ('id', 'PK'), ('name', ''), ('email', 'UQ'),
    ('email_verified_at', ''), ('password', ''),
    ('remember_token', ''), ('created_at', ''), ('updated_at', ''),
]
draw_table(ax, 0.5, 8.8, 3.8, 'users', users)

# ── EVENTS (centre-top) ──────────────────────────────────────────
events = [
    ('id', 'PK'), ('title', ''), ('date', ''),
    ('time', ''), ('location', ''), ('created_at', ''), ('updated_at', ''),
]
draw_table(ax, 5.1, 8.8, 3.8, 'events', events)

# ── REGISTRATIONS (centre-bottom) ────────────────────────────────
regs = [
    ('id', 'PK'), ('event_id', 'FK'), ('student_id', ''),
    ('name', ''), ('email', ''), ('qr_token', 'UQ'),
    ('checked_in_at', ''), ('created_at', ''), ('updated_at', ''),
]
draw_table(ax, 5.1, 4.5, 3.8, 'registrations', regs)

# ── RELATIONSHIPS ────────────────────────────────────────────────
# events.id (PK) → registrations.event_id (FK)  1:N  straight down
events_bottom = 8.8 - (HDR_H + 7 * ROW_H)   # bottom of events
regs_top      = 4.5
mid_x         = 7.0  # centre of both tables

ax.plot([mid_x, mid_x], [events_bottom, regs_top], color='#E74C3C', lw=2, zorder=5)
ax.annotate('', xy=(mid_x, regs_top), xytext=(mid_x, regs_top + 0.18),
            arrowprops=dict(arrowstyle='-|>', color='#E74C3C', lw=2, mutation_scale=15), zorder=5)
ax.text(mid_x + 0.15, (events_bottom + regs_top) / 2, '1 : N',
        ha='left', va='center', fontsize=9, fontweight='bold', color='#E74C3C',
        bbox=dict(facecolor='white', edgecolor='#E74C3C', boxstyle='round,pad=0.2', lw=0.8), zorder=6)

# ── TITLE ────────────────────────────────────────────────────────
ax.text(7.0, 9.8, 'ER Diagram — Event Registration & Attendance System',
        ha='center', va='center', fontsize=13, fontweight='bold', color='#2C3E50')

# ── LEGEND ───────────────────────────────────────────────────────
legend_items = [
    ('#E67E22', 'PK  Primary Key'),
    ('#2980B9', 'FK  Foreign Key'),
    ('#27AE60', 'UQ  Unique'),
]
for i, (c, lbl) in enumerate(legend_items):
    ax.text(0.5 + i * 2.6, -0.68, lbl, ha='left', va='center',
            fontsize=8.5, color=c, fontweight='bold')

plt.tight_layout(pad=0.5)
plt.savefig('/home/user/Event-Registration-and-Attendance-Information-System/er_diagram.png',
            dpi=180, bbox_inches='tight', facecolor='white')
print("Done.")
