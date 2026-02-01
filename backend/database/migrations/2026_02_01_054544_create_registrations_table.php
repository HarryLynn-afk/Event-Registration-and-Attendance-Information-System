<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('registrations', function (Blueprint $table) {
            $table->id();
            $table->foreignId('event_id')->constrained()->onDelete('cascade');
            $table->string('student_id');
            $table->string('name');
            $table->string('email');
            $table->string('qr_token')->unique();
            $table->timestamp('checked_in_at')->nullable();
            $table->timestamps();
            
            // Unique constraint: one registration per student per event
            $table->unique(['event_id', 'student_id']);
            
            // Index on qr_token for fast lookups
            $table->index('qr_token');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('registrations');
    }
};
